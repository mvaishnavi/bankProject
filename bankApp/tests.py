from django.test import TestCase, Client
import factory
from .models import Banks, Branches
from django.urls import reverse


class BanksFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Banks

    name = factory.Sequence(lambda n: u'Banks {}'.format(n))
    id = factory.Sequence(lambda n: n+1)


class BranchesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Branches

    bank = factory.SubFactory(BanksFactory)
    branch = factory.Sequence(lambda n: 'Branches {}'.format(n))
    ifsc = factory.Sequence(lambda n: 'IFSC000001{}'.format(n))
    address = factory.Sequence(lambda n: 'Address {}'.format(n))
    city = 'City'
    state = factory.Sequence(lambda n: 'State {}'.format(n))
    district = factory.Sequence(lambda n: 'District {}'.format(n))

client = Client()


class GetIfscTest(TestCase):
    
    def setUp(self):

        self.main_bank = BanksFactory()
        self.head_office = BranchesFactory.create(bank=self.main_bank)

    def test_get_ifsc_page(self):

        response = client.get(reverse('get_ifsc_page'))
        self.assertContains(response, 'Enter IFSC to get details')
        self.assertEqual(response.context[0]['object']['object'], None)


    def test_get_ifsc_page_wrong_ifsc(self):

        response = client.get(reverse('get_ifsc_details', kwargs={'ifsc':'ICIC0000035'}))
        self.assertContains(response, 'Entered IFSC does not exist.')
        self.assertEqual(response.context[0]['object']['object'], None)


class GetBranchesTest(TestCase):

    def setUp(self):

        self.main_bank = BanksFactory()
        self.head_office = BranchesFactory.create(bank=self.main_bank)

    def test_get_branch_list_by_bank_id(self):

        response = client.get(reverse('get_branch_list', kwargs={'bank_id':self.main_bank.id}))
        self.assertContains(response, '1 pages of branches found for '+self.main_bank.name)
        self.assertEqual(len(response.context[0]['branches']), 1)


    def test_get_branch_list_by_city_no_branches_case(self):

        response = client.get(reverse('get_branch_list_by_city', kwargs={'bank_id':self.main_bank.id, 'city':'abcd'}))
        self.assertContains(response, 'No branches found for '+self.main_bank.name+' in abcd.')
        self.assertEqual(len(response.context[0]['branches']), 0)


    def test_get_branch_list_by_city_success_case(self):

        response = client.get(reverse('get_branch_list_by_city', kwargs={'bank_id':self.main_bank.id, 'city':self.head_office.city}))
        self.assertContains(response, '1 pages of branches found for '+self.main_bank.name+' in '+self.head_office.city+'.')
        self.assertEqual(len(response.context[0]['branches']), 1)


    def test_get_branch_list_by_city_no_bank_id_case(self):

        response = client.get(reverse('get_branch_page'))
        self.assertEqual(response.context[0]['error'], 'Choose a bank')
        self.assertEqual(len(response.context[0]['branches']), 0)


    def test_get_branch_list_by_city_wrong_bank_id_case(self):

        response = client.get(reverse('get_branch_list_by_city', kwargs={'bank_id':11111, 'city':self.head_office.city}))
        self.assertEqual(response.context[0]['error'], 'Chosen bank does not exist.')
        self.assertEqual(len(response.context[0]['branches']), 0)



